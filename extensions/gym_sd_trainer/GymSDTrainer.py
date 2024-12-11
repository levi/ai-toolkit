from collections import OrderedDict
from extensions_built_in.sd_trainer.SDTrainer import SDTrainer
from typing import TYPE_CHECKING, Optional, Callable

if TYPE_CHECKING:
    from jobs import ExtensionJob


class GymSDTrainer(SDTrainer):
    def __init__(
        self, process_id: int, job: "ExtensionJob", config: OrderedDict, **kwargs
    ):
        super().__init__(process_id, job, config, **kwargs)

    def post_save_hook(self, save_path: str):
        """Called after a model is saved"""
        super().post_save_hook(save_path)
        save_callback = self.get_conf("save_callback")
        if save_callback:
            save_callback(save_path)
