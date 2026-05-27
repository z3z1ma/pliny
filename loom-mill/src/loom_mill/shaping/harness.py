from __future__ import annotations

import asyncio
import inspect
import os
import time
from collections.abc import Awaitable, Callable
from dataclasses import dataclass, field


StreamCallback = Callable[[str], None | Awaitable[None]]


@dataclass(frozen=True)
class InvocationConfig:
    goal: str
    context_excerpt: str
    command: str
    args: list[str] = field(default_factory=list)
    env: dict[str, str] = field(default_factory=dict)
    cwd: str | None = None
    timeout_seconds: float = 120.0


@dataclass(frozen=True)
class InvocationResult:
    invocation_id: str
    goal: str
    exit_code: int
    output: str
    stderr: str
    duration_seconds: float
    context_summary: str


def build_prompt(goal: str, context_excerpt: str) -> str:
    return f"""# Exploration Goal

{goal}

# Session Context (relevant excerpt)

{context_excerpt}

# Instructions

Explore the goal above. You have full filesystem access.
When done, end your output with:

## Summary

<concise summary of what you discovered>
"""


def extract_context_summary(output: str) -> str:
    marker = "## Summary"
    index = output.rfind(marker)
    if index == -1:
        return ""
    return output[index + len(marker) :].strip()


async def run_bounded_invocation(
    config: InvocationConfig,
    invocation_id: str,
    on_stream: StreamCallback | None = None,
    prompt_override: str | None = None,
) -> InvocationResult:
    if not config.command.strip():
        raise ValueError("harness command is required")

    started = time.monotonic()
    env = os.environ.copy()
    env.update(config.env)
    proc = await asyncio.create_subprocess_exec(
        config.command,
        *config.args,
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        cwd=config.cwd or os.getcwd(),
        env=env,
    )

    stdout_parts: list[str] = []
    stderr_parts: list[str] = []

    async def maybe_stream(line: str) -> None:
        if on_stream is None:
            return
        result = on_stream(line)
        if inspect.isawaitable(result):
            await result

    async def read_stdout() -> None:
        if proc.stdout is None:
            return
        while line := await proc.stdout.readline():
            text = line.decode("utf-8", errors="replace")
            stdout_parts.append(text)
            await maybe_stream(text)

    async def read_stderr() -> None:
        if proc.stderr is None:
            return
        while chunk := await proc.stderr.read(4096):
            stderr_parts.append(chunk.decode("utf-8", errors="replace"))

    stdout_task = asyncio.create_task(read_stdout())
    stderr_task = asyncio.create_task(read_stderr())
    timed_out = False

    try:
        assert proc.stdin is not None
        prompt = prompt_override if prompt_override is not None else build_prompt(config.goal, config.context_excerpt)
        proc.stdin.write(prompt.encode("utf-8"))
        await proc.stdin.drain()
        proc.stdin.close()
        await proc.stdin.wait_closed()

        try:
            await asyncio.wait_for(proc.wait(), timeout=config.timeout_seconds)
        except TimeoutError:
            timed_out = True
            proc.kill()
            await proc.wait()

        await asyncio.gather(stdout_task, stderr_task)
    except asyncio.CancelledError:
        if proc.returncode is None:
            proc.kill()
            await proc.wait()
        await asyncio.gather(stdout_task, stderr_task, return_exceptions=True)
        raise
    except Exception:
        if proc.returncode is None:
            proc.kill()
            await proc.wait()
        await asyncio.gather(stdout_task, stderr_task, return_exceptions=True)
        raise

    output = "".join(stdout_parts)
    stderr = "".join(stderr_parts)
    if timed_out:
        stderr = (stderr + "\n" if stderr else "") + f"Timed out after {config.timeout_seconds} seconds"
    return InvocationResult(
        invocation_id=invocation_id,
        goal=config.goal,
        exit_code=proc.returncode if proc.returncode is not None else -1,
        output=output,
        stderr=stderr,
        duration_seconds=time.monotonic() - started,
        context_summary=extract_context_summary(output),
    )
