from vc_wrap import SvetObject
from combine_runs import ConstraintObject

# value stacking, should be the best scenario
caiso_all = SvetObject(SVet_absolute_path="/Applications/storagevet2v101/StorageVET-master-git/",
                       default_params_file="Model_Parameters_2v1-0-2_default_03-2021.csv",
                       shortname="CAISO DCM+SR+NSR on",
                       description="CAISO",
                       Scenario_n="48",
                       Scenario_time_series_filename="/Users/zhenhua/Desktop/price_data/hourly_timeseries_2019.csv",
                       Finance_customer_tariff_filename="/Users/zhenhua/Desktop/price_data/tariff_data/original_documents/caiso_pge_b20_2020.csv",
                       DCM_active='yes',
                       retailTimeShift_active='yes',
                       DA_active='no',
                       SR_active='yes',
                       NSR_active='yes',
                       FR_active="no",
                       FR_CombinedMarket="1"
                       )
caiso_all.run_storagevet()

# use ths to determine monthly peak net load
caiso_baseline = SvetObject(SVet_absolute_path="/Applications/storagevet2v101/StorageVET-master-git/",
                            default_params_file="Model_Parameters_2v1-0-2_default_03-2021.csv",
                            shortname="CAISO DCM+SR on",
                            description="CAISO",
                            Scenario_n="48",
                            Scenario_time_series_filename="/Users/zhenhua/Desktop/price_data/hourly_timeseries_2019.csv",
                            Finance_customer_tariff_filename="/Users/zhenhua/Desktop/price_data/tariff_data/original_documents/caiso_pge_b20_2020.csv",
                            DCM_active='yes',
                            retailTimeShift_active='yes',
                            DA_active='no',
                            SR_active='no',
                            NSR_active='no',
                            FR_active="no",
                            FR_CombinedMarket="1"
                            )
caiso_baseline.run_storagevet()

# DCM constraints
DCMconstraint = ConstraintObject(SVet_absolute_path="/Applications/storagevet2v101/StorageVET-master-git/",
                                 shortname=caiso_baseline.shortname, baseline_runID=caiso_baseline.runID,
                                 app_hours=[0, 23],
                                 regulation_scenario=1,
                                 constraint_init=True)
DCMconstraint.set_DCM_user_constraints()

# determine sr constraints
caiso_all_w_dcm = SvetObject(SVet_absolute_path="/Applications/storagevet2v101/StorageVET-master-git/",
                             default_params_file="Model_Parameters_2v1-0-2_default_03-2021.csv",
                             shortname=DCMconstraint.new_shortname,
                             description="CAISO",
                             Scenario_n="48",
                             Scenario_time_series_filename=DCMconstraint.new_hourly_timeseries_path,
                             Finance_customer_tariff_filename="/Users/zhenhua/Desktop/price_data/tariff_data/original_documents/caiso_pge_b20_2020.csv",
                             User_active="yes", User_price=DCMconstraint.values,
                             DCM_active='no',
                             retailTimeShift_active='yes',
                             DA_active='no',
                             SR_active='yes',
                             NSR_active='yes',
                             FR_active="no",
                             FR_CombinedMarket="1"
                             )
caiso_all_w_dcm.run_storagevet()

# SR has priority from 2-8pm
SRconstraint = ConstraintObject(SVet_absolute_path="/Applications/storagevet2v101/StorageVET-master-git/",
                                shortname=caiso_all_w_dcm.shortname, baseline_runID=caiso_all_w_dcm.runID,
                                app_hours=[14, 19],
                                regulation_scenario=3,
                                constraint_init=True)
SRconstraint.set_SR_user_constraints()

caiso_sr_priority = SvetObject(SVet_absolute_path="/Applications/storagevet2v101/StorageVET-master-git/",
                               default_params_file="Model_Parameters_2v1-0-2_default_03-2021.csv",
                               shortname=SRconstraint.new_shortname,
                               description="CAISO",
                               Scenario_n="48",
                               Scenario_time_series_filename=SRconstraint.new_hourly_timeseries_path,
                               Finance_customer_tariff_filename="/Users/zhenhua/Desktop/price_data/tariff_data/original_documents/caiso_pge_b20_2020.csv",
                               User_active="yes", User_price=SRconstraint.values,
                               DCM_active='no',
                               retailTimeShift_active='yes',
                               DA_active='no',
                               SR_active='no',
                               NSR_active='yes',
                               FR_active="no",
                               FR_CombinedMarket="1"
                               )
caiso_sr_priority.run_storagevet()

caiso_sr_priority = SvetObject(SVet_absolute_path="/Applications/storagevet2v101/StorageVET-master-git/",
                               default_params_file="Model_Parameters_2v1-0-2_default_03-2021.csv",
                               shortname=SRconstraint.new_shortname,
                               description="CAISO",
                               Scenario_n="48",
                               Scenario_time_series_filename=SRconstraint.new_hourly_timeseries_path,
                               Finance_customer_tariff_filename="/Users/zhenhua/Desktop/price_data/tariff_data/original_documents/caiso_pge_b20_2020.csv",
                               User_active="yes", User_price=SRconstraint.values,
                               DCM_active='yes',
                               retailTimeShift_active='yes',
                               DA_active='no',
                               SR_active='no',
                               NSR_active='yes',
                               FR_active="no",
                               FR_CombinedMarket="1"
                               )
caiso_sr_priority.run_storagevet()
