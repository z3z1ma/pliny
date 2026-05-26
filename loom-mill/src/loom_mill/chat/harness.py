from __future__ import annotations

import asyncio
import os
import shlex
from collections.abc import Awaitable, Callable


async def run_harness(
    command: str,
    prompt: str,
    session_id: str,
    broadcast_fn: Callable[[dict], Awaitable[None]],
) -> str:
    """Spawn harness, stream output via broadcast_fn, and return the full response."""
    args = shlex.split(command)
    if not args:
        raise ValueError("harness command is required")

    stdin = None
    if "opencode" in args[0]:
        args.extend(["-m", prompt])
    else:
        stdin = asyncio.subprocess.PIPE

    proc = await asyncio.create_subprocess_exec(
        *args,
        stdin=stdin,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        cwd=os.getcwd(),
    )

    if stdin is not None and proc.stdin is not None:
        proc.stdin.write(prompt.encode("utf-8"))
        await proc.stdin.drain()
        proc.stdin.close()

    full_response: list[str] = []
    assert proc.stdout is not None
    async for line in proc.stdout:
        text = line.decode("utf-8", errors="replace")
        full_response.append(text)
        await broadcast_fn(
            {
                "event": "chat_stream",
                "data": {"session_id": session_id, "delta": text, "done": False},
            }
        )

    stderr = b""
    if proc.stderr is not None:
        stderr = await proc.stderr.read()
    await proc.wait()

    if proc.returncode != 0:
        error = stderr.decode("utf-8", errors="replace").strip() or f"Harness exited with {proc.returncode}"
        await broadcast_fn({"event": "chat_error", "data": {"session_id": session_id, "error": error}})
        raise RuntimeError(error)

    response_text = "".join(full_response)
    await broadcast_fn(
        {
            "event": "chat_complete",
            "data": {"session_id": session_id, "message": {"role": "assistant", "content": response_text}},
        }
    )
    return response_text
