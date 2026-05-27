import asyncio
import signal
from collections.abc import Sequence


async def run_process(command: Sequence[str]) -> int:
    process = await asyncio.create_subprocess_exec(*command)
    try:
        return await process.wait()
    except asyncio.CancelledError:
        process.send_signal(signal.SIGTERM)
        await process.wait()
        raise


async def run_dev_stack() -> int:
    backend = asyncio.create_task(
        run_process(
            [
                "uvicorn",
                "loom_mill.app:app",
                "--reload",
                "--host",
                "127.0.0.1",
                "--port",
                "8765",
            ]
        )
    )
    frontend = asyncio.create_task(
        run_process(
            [
                "npm",
                "--prefix",
                "frontend",
                "run",
                "dev",
                "--",
                "--host",
                "127.0.0.1",
            ]
        )
    )
    tasks = {backend, frontend}
    done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
    for task in pending:
        task.cancel()
    await asyncio.gather(*pending, return_exceptions=True)
    return next(iter(done)).result()


def main() -> None:
    raise SystemExit(asyncio.run(run_dev_stack()))


if __name__ == "__main__":
    main()
