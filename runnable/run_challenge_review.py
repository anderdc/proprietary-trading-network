from matplotlib import pyplot as plt
import time

from vali_objects.scoring.scoring import Scoring
from vali_objects.utils.logger_utils import LoggerUtils
from vali_objects.utils.subtensor_weight_setter import SubtensorWeightSetter
from vali_objects.utils.vali_bkp_utils import ValiBkpUtils
from vali_objects.utils.vali_utils import ValiUtils
from time_util.time_util import TimeUtil

if __name__ == "__main__":
    logger = LoggerUtils.init_logger("run incentive review")

    subtensor_weight_setter = SubtensorWeightSetter(None, None, None)

    hotkeys = ValiBkpUtils.get_directories_in_dir(ValiBkpUtils.get_miner_dir())

    eliminations_json = ValiUtils.get_vali_json_file(
        ValiBkpUtils.get_eliminations_dir()
    )["eliminations"]

    current_time = TimeUtil.now_in_millis()

    # Get all possible positions, even beyond the lookback range
    challengeperiod_results = subtensor_weight_setter.challenge_period_screening(
        hotkeys,
        current_time=current_time,
        eliminations=eliminations_json,
        log=True,
    )

    eliminated_keys = [ x['hotkey'] for x in eliminations_json ]

    challengeperiod_miners = challengeperiod_results['challengeperiod_miners']
    challengeperiod_eliminations = challengeperiod_results['challengeperiod_eliminations']
    existing_positions = set(hotkeys) - set(challengeperiod_miners) - set(challengeperiod_eliminations) - set(eliminated_keys)

    time.sleep(1)
    logger.info(f"{len(challengeperiod_miners)} challengeperiod_miners [{challengeperiod_miners}]")
    logger.info(f"{len(challengeperiod_eliminations)} challengeperiod_eliminations [{challengeperiod_eliminations}]")
    logger.info(f"{len(list(existing_positions))} challenge period pass [{list(existing_positions)}]")