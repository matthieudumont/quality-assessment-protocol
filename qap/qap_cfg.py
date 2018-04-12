default_pipeline_configuration = {
    'log_directory': '',
    'output_directory': '',
    'working_directory': '/tmp',
    'save_working_dir': False,
    'recompute_all_derivatives': False,
    's3_read_credentials': '',
    's3_write_credentials': '',
    'anatomical_template': '/opt/afni/MNI_avg152T1+tlrc',
    'exclude_zeros': 'False',
    'functional_start_index': '0',
    'functional_stop_index': 'End',
    'bundle_size': 1,
    'num_processors': 1,
    'available_memory': 4,
    'write_report': False,
    'write_graph': False
}

configuration_output_string = """
    Pipeline Configuration
    ----------------------

    Log directory:          {log_directory}
    Output directory:       {output_directory}
    Working directory:      {working_directory}
    ---
    Save working directory: {save_working_dir}
    Recompute everything:   {recompute_all_derivatives}
    ---
    S3 input credentials:   {s3_read_credentials}
    S3 output credentials:  {s3_write_credentials}
    ---
    MNI template:           {anatomical_template}
    Exclude zeros:          {exclude_zeros}
    Start index:            {functional_start_index}
    Stop index:             {functional_stop_index}
    ---
    Bundle size:            {bundle_size}
    Number of processors:   {num_processors}
    Memory (GB):            {available_memory}
    ---
    Write report:           {write_report}

    Write execution graph:  {write_graph}
"""


def write_pipeline_configuration(configuration_output_filename, configuration_dictionary):
    """ Write out a config file with the parameters in config_dict.

        This would be a lot easier to just use yaml.dump, but we want the
        configuration file to be human readable and to include comments. The
        latter is not currently supported by pyYaml. Maybe in the future?

    :type configuration_output_filename: str
    :param configuration_output_filename: Filename, including path, of the file to be written
    :type configuration_dictionary: dict
    :param configuration_dictionary: configuration dictionary (see config_dict defined above)
                        that contains the parameters to be written to the config file
    :return: nothing
    """

    configuration_file_string = '''
# Preprocessed Connectomes Project Quality Assessment Protocol (QAP)
# Configuration file
#
#
# QAP Parameters
# --------------
#
# Path to a whole head template. This is only required if you are processing sMRI data. The default
# is the MNI2mm template distributed with AFNI, but you are free to use any that you choose.
anatomical_template: {anatomical_template}

# Many of the QAP measures use background voxels to calculate surrogate measures of noise. If some
# of those voxels have been arbitrarily set to zero, by defacing for anonymization or other reasons,
# it will bias these measures. These voxels can be ignored by setting the following flag to `True'
exclude_zeros: {exclude_zeros}

# The first few volumes of an fMRI scan may have different signal properties due to T1 equilibrium
# effects. Set this parameter to discard volumes from the beginning of the scan.
functional_start_index: {functional_start_index}

# Similarly it may be desirable to exclude volumes at the end of the scan from the calculation. Set
# this parameter to the index of the last volume to include in calculations, or 'End' for the last volume.
functional_stop_index: {functional_stop_index}

# Set the write_report parameter to True if you would like QAP to produce PDF reports visualizing the
# results of the QAP metrics.
write_report: {write_report}


# Output Paths:
# -------------
#
# Directory for outputs generated by QAP. This includes a single JSON for each sMRI scan and a JSON for
# each fMRI scan. To write outputs directly to the AWS S3 cloud service prepend the output path with
# s3://bucket_name/". This may require setting s3_write_credentials (next section)
output_directory: {output_directory}

# Directory for log files. To upload log files to the AWS S3 cloud service prepend the output path with
# s3://bucket_name/". This may require setting s3_write_credentials (next section)
log_directory: {log_directory}


# Calculating the QAP measures requires  a variety of intermediary files that are derived from the input
# data (e.g., brain mask, white matter mask). These files are written to a working directory that can be
# automatically deleted when QAP completes. Since a lot of files will be written and read from this directory,
# it should ideally be locally connected to the workstation (i.e. not a network share) - this is especially
# important for cluster and cloud based calculation.
working_directory: {working_directory}

# When QAP begins execution it will scan the input and output directory structures for files from previous
# runs of QAP and use those as available. This is meant to be a time saving measure. If you want QAP to
# ignore existing files and recompute everything, set this flag to True
recompute_all_derivatives: {recompute_all_derivatives}

# AWS S3 Credentials
#-------------------
#
# AWS credentials may be needed if reading data from S3, if so edit the path to point to the credential
# file downloaded from AWS. If unset, and s3 paths are encountered, QAP will try to download the data anonymously.
s3_read_credentials: {s3_read_credentials}

# AWS credentials will probably be needed if writing to S3, if so edit the path to point to the credential
# file downloaded from AWS. If unset, and s3 paths are encountered, QAP will try to upload the data anonymously.
s3_write_credentials: {s3_write_credentials}


# Multicore Parallelization and Bundles
# -------------------------------
#
# The different procedures that are required to calculate QAP measures from
# a dataset (sMRI or fMRI) is represented as a node in the QAP pipeline. Each
# dataset has a separate pipeline that can be executed in parallel using multi-core
# and cluster -based parallelization to achieve high throughput.

# For multicore parallelization, QAP relies on Nipype to execute different steps of
# the pipeline in parallel on the processors available on a single workstation. The
# number of nodes that can be scheduled to execute in parallel is limited by the total
# number of processors and amount of RAM available on the system. Practically the
# amount of parallelization that can be achieved is limited by the dependencies pipeline
# steps. For example, several nodes of the pipeline can be blocked until a node produces
# an intermediary file that they all need. QAP mitigates this problem by combining
# pipelines into a 'bundle' so that pipeline steps for different data can execute
# in parallel. We bundle data by session to simplify balancing the number of sMRI
# and fMRI data but into each bundle. So the bundle size is in units of sessions. In
# other words, if in your dataset you have two sessions per participant and each session
# contains two fMRI and one sMRI scans, and you specify a bundle size of 10, each bundle
# will receive 10 sMRI and 20 fMRI scans.
#
# When no other resource constrains execution, it may work best to put all of the data
# into a single bundle and allow them to all compete for unused resources. Since intermediary
# files must be retained until a pipeline completes, the space required to store these
# files limits the number of pipelines that can be run in parallel. The working directory
# for structural and functional data are estimated to require about twice the input data
# size in storage. The max bundle size you should use can be estimated from:
#    (size of working dir) / ( twice size of bundle )
# In the previous example the bundle size would be the size of one sMRI plus the two fMRI
# scans.
#
# The parameter below specifies the bundle size to use.
bundle_size: {bundle_size}

# The following parameters specify the number of processors and amount of memory (in GB) that are
# available for multicore processing. If using cluster computing, these are the resources
# available on each cluster node.
num_processors: {num_processors}
available_memory: {available_memory}


# Debugging
# -------------------------------
# If you do not want to automatically delete the working directory at the end of QAP, change the following
# flag to `True'.
save_working_dir: {save_working_dir}


# Produce a graph for visualizing the workflow
write_graph: {write_graph}
    '''

    with open(configuration_output_filename, 'w') as ofd:
        ofd.write(configuration_file_string.format(**configuration_dictionary))

    return 1


def validate_pipeline_configuration(pipeline_configuration):
    """
    Validate the pipeline configuration dictionary to ensure the
    parameters are properly set.
    :param pipeline_configuration:
    :return:
    """

    required_configuration_parameters = ['anatomical_template',
                                         'exclude_zeros',
                                         'functional_start_index',
                                         'functional_stop_index',
                                         'bundle_size',
                                         'num_processors',
                                         'available_memory',
                                         'output_directory',
                                         'working_directory',
                                         'log_directory',
                                         's3_read_credentials',
                                         's3_write_credentials',
                                         'save_working_dir',
                                         'recompute_all_derivatives',
                                         'write_report',
                                         'write_graph'

                                         ]

    missing_parameters = []
    for parameter in required_configuration_parameters:
        if parameter not in pipeline_configuration:
            missing_parameters.append(parameter)

    if len(missing_parameters) > 0:
        error_string = '\n[!] The following rquired parameters are missing from the pipeline configuration:'
        error_string += ",".join([parameter for parameter in missing_parameters]) + '\n'
        raise Exception(error_string)

if __name__ == "__main__":
    write_pipeline_configuration("test_config.yml", default_pipeline_configuration)

    print(configuration_output_string.format(**default_pipeline_configuration))

    import yaml

    test_configuration = yaml.load(open("test_config.yml", "r"))
    print(configuration_output_string.format(**test_configuration))

    validate_pipeline_configuration(test_configuration)
    validate_pipeline_configuration(default_pipeline_configuration)

    assert(test_configuration != default_pipeline_configuration)