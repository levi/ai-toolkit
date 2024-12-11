from toolkit.extension import Extension


class GymSDTrainerExtension(Extension):
    uid = "gym_sd_trainer"
    name = "Gym SD Trainer"

    @classmethod
    def get_process(cls):
        from .GymSDTrainer import GymSDTrainer

        return GymSDTrainer


AI_TOOLKIT_EXTENSIONS = [GymSDTrainerExtension]
