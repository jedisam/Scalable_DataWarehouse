"""
Copyright 2020, Olger Siebinga (o.siebinga@tudelft.nl)
This file is part of Travia.
Travia is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
Travia is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with Travia.  If not, see <https://www.gnu.org/licenses/>.
"""
import argparse
import datetime
import sys
import warnings

from PyQt5 import QtWidgets

from dataobjects import PNeumaDataset, NGSimDataset, HighDDataset, ExiDDataset
from dataobjects.enums import (
    DataSource,
    HighDDatasetID,
    NGSimDatasetID,
    PNeumaDatasetID,
    ExiDDatasetID,
)
from gui import TrafficVisualizerGui, DatasetSelectionDialog
from visualisation import (
    NGSimVisualisationMaster,
    HighDVisualisationMaster,
    PNeumaVisualisationMaster,
    ExiDVisualisationMaster,
)


def visualize_traffic_data(data, dataset_id, app):
    gui = TrafficVisualizerGui(data)

    if dataset_id.data_source == DataSource.NGSIM:
        start_time = datetime.datetime.fromtimestamp(
            int(data.track_data.loc[:, "Global_Time"].min() / 1000)
        )
        end_time = datetime.datetime.fromtimestamp(
            int(data.track_data.loc[:, "Global_Time"].max() / 1000)
        )
        first_frame = data.track_data.loc[:, "Frame_ID"].min()
        number_of_frames = data.track_data.loc[:, "Frame_ID"].max() - first_frame
        visualisation_master = NGSimVisualisationMaster(
            data, gui, start_time, end_time, number_of_frames, first_frame
        )
    elif dataset_id.data_source in [DataSource.HIGHD, DataSource.EXID]:
        start_time = data.start_time
        end_time = start_time + datetime.timedelta(
            milliseconds=int(data.duration * 1000)
        )
        first_frame = data.track_data["frame"].min()
        number_of_frames = data.track_data["frame"].max() - first_frame
        dt = datetime.timedelta(seconds=1 / data.frame_rate)
        if dataset_id.data_source is DataSource.HIGHD:
            visualisation_master = HighDVisualisationMaster(
                data, gui, start_time, end_time, number_of_frames, first_frame, dt
            )
        else:
            visualisation_master = ExiDVisualisationMaster(
                data, gui, start_time, end_time, number_of_frames, first_frame, dt
            )
    elif dataset_id.data_source == DataSource.PNEUMA:
        visualisation_master = PNeumaVisualisationMaster(
            data,
            gui,
            data.start_time,
            data.end_time,
            data.number_of_frames,
            0,
            data.dt * 2,
            default_frame_step=2,
        )
    else:
        raise ValueError(
            "No alternative is implemented for this data source. Is it a new data source?"
        )

    gui.register_visualisation_master(visualisation_master)

    exit_code = app.exec_()
    data.save()
    sys.exit(exit_code)


def get_dataset_id_from_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-s",
        "--source",
        type=str,
        choices=["highd", "ngsim", "pneuma"],
        help="The data source, one of highd, ngsim, pneuma",
        required=False,
    )
    parser.add_argument(
        "-d", "--dataset", type=str, help="The dataset id", required=False,
    )
    known_args, other_args = parser.parse_known_args()

    try:
        if known_args.source == "highd":
            dataset_id = HighDDatasetID[known_args.dataset]
        elif known_args.source == "ngsim":
            dataset_id = NGSimDatasetID[known_args.dataset]
        elif known_args.source == "pneuma":
            dataset_id = PNeumaDatasetID[known_args.dataset]
        else:
            dataset_id = None
    except KeyError:
        warnings.warn("Invalid dataset source and ID combination provided")
        dataset_id = None

    return dataset_id, other_args


def get_dataset_id_from_dialog(qt_args):
    data_selection_app = QtWidgets.QApplication(qt_args)
    dataset_selection_dialog = DatasetSelectionDialog()
    data_selection_app.exec_()
    return dataset_selection_dialog.selected_dataset_id


if __name__ == "__main__":
    """
    To visualise data, you need to define the dataset ID. These ID's are predefined in enums and contain information like the file path for the data and images.
    With this ID, it is possible to load the dataset. All projects have their own enum for ID's and class for datasets. Please look at the examples below to see
    how to load a dataset. 
    """

    "For direct loading of a HighD dataset, uncomment the next line: "
    # dataset_id = HighDDatasetID.DATASET_01
    "For direct loading of an NGSIM dataset, uncomment the next line: "
    # dataset_id = NGSimDatasetID.US101_0805_0820
    "For direct loading of a PNeuma dataset, uncomment the next line: "
    # dataset_id = PNeumaDatasetID.D181029_T1000_1030_DR8
    "For direct loading of an ExiD dataset, uncomment the next line: "
    # dataset_id = ExiDDatasetID.DATASET_26

    # check if a dataset id was provided in arguments, if so: overrule the id above
    id_from_arguments, other_args = get_dataset_id_from_arguments()

    if id_from_arguments is not None:
        dataset_id = id_from_arguments

    # if no dataset is selected yet, prompt the user with a dialog to select a dataset
    try:
        dataset_id
    except NameError:
        dataset_id = get_dataset_id_from_dialog(other_args)

    if dataset_id is None:
        exit(0)

    # load data and start
    main_app = QtWidgets.QApplication(other_args)

    if dataset_id.data_source == DataSource.HIGHD:
        data = HighDDataset.load(dataset_id)
    elif dataset_id.data_source == DataSource.NGSIM:
        data = NGSimDataset.load(dataset_id)
    elif dataset_id.data_source == DataSource.PNEUMA:
        data = PNeumaDataset.load(dataset_id)
    elif dataset_id.data_source == DataSource.EXID:
        data = ExiDDataset.load(dataset_id)
    else:
        raise ValueError(
            "No alternative is implemented for this data source. Is it a new data source?"
        )

    visualize_traffic_data(data, dataset_id, main_app)
