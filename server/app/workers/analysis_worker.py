import logging
from multiprocessing import Queue
from typing import Any

logger = logging.getLogger(__name__)


class AnalysisWorker:
    """Runs CPU-intensive frame analysis tasks in a separate process."""

    def __init__(self) -> None:
        pass

    def run(
        self,
        frames: list[str],
        result_queue: "Queue[Any]",
        progress_queue: "Queue[Any]",
    ) -> list[Any]:
        """Process a list of frame paths and push results to result_queue.

        Progress updates are emitted to progress_queue as each frame completes.
        """
        logger.info("AnalysisWorker.run called with %d frames", len(frames))
        return []
