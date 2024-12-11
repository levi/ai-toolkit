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
        # Print full config for debugging
        print("Full config:")
        print(self.config)

        # Get and debug the callback function from config
        self.save_callback: Optional[Callable[[str], None]] = self.get_conf(
            "save_callback"
        )
        print("Save callback value:", self.save_callback)
        print("Save callback type:", type(self.save_callback))

    def post_save_hook(self, save_path: str):
        """Called after a model is saved"""
        super().post_save_hook(save_path)
        print(f"Post save hook called for path: {save_path}")
        if self.save_callback:
            print("Executing save callback")
            self.save_callback(save_path)
            print("Save callback completed")
