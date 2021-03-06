#  Copyright (c) 2021. Harvard University
#
#  Developed by Research Software Engineering,
#  Faculty of Arts and Sciences, Research Computing (FAS RC)
#  Author: Ben Sabath
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#

# Functions for handling basic interpolation

import numpy as np


def interpolate_ma(num_vec: np.array, k: int):
    """
    Python implementation of the logic described in the function located at:
    https://github.com/SteffenMoritz/imputeTS/blob/master/R/na_ma.R

    If all inputs are missing, we return only missing values

    :param num_vec: Numeric vector with some missing values
    :param k: minimum number of observations on each side of hte missing value to include in the
        weighted mean.

    :return: a np.array where the missing values have been replaced by new values calculated from a
        rolling average imputation method.


    """

    # What does the function do
    # Default method uses exponential weighitng, need to re-implement that

    # 1. Creates a copy of input vector to maintian unreplaced data
    # 2. Creates a copy to fill the missing data in
    with_missing = np.array(num_vec)
    out = with_missing.copy()

    # Handle case of not enough data
    # if everything is missing, can't replace any values
    # If only one value present, set everything to that value
    num_with_data = len(with_missing) - np.sum(np.isnan(with_missing))
    if num_with_data == 0:
        return out
    elif num_with_data == 1:
        out[np.argwhere(np.isnan(with_missing))] = np.nanmean(with_missing)
        return out

    # For each value in the input vector
    # check to see if it's missing.

    for i in range(len(with_missing)):
        if not np.isnan(with_missing[i]):
            continue

        # Calculate vector of weights for the mean
        # Default is exponential weights, based on distance from the value in question
        # Weights = 2**abs(index - i). missing values weighted at 0
        # Calculate weighted mean of selected values, fill in missing value

        indices = get_indices(with_missing, i, k)
        weights = calc_weights(with_missing, indices, i)
        window = with_missing[indices]
        window = np.nan_to_num(window)  # replace nan with missing to allow for dot product
        out[i] = window.dot(weights) / np.sum(weights)

    return out


def get_indices(vec, index, k):
    """
    Return a range object of the indices to be used to calculate a rolling mean
    If the window defined by ``k`` doesn't contain at least 2 non-missing values,
    k is increased by one until the window has at least two non-missing values.

    :param vec: np.array with missing data
    :param k: minimum window on either side
    :param index: Index to center the window around
    :return: np.array containing the indices defining the window


    """

    while True:
        out = np.array(range(max(0, index - k), min(len(vec), index + k + 1)))
        if len(out) - np.sum(np.isnan(vec[out])) >= 2:
            return out
        else:
            k += 1


def calc_weights(vec, indices, i):
    """
    Create an array of weights for an array of indices, with the weight decreasing exponentially with distance
    from index of interest ``i``. Indices pointing to missing data have their weight set to 0.

    :param vec: np.array of data being interpolated, known to have missingness.
    :param indices: array of indices generated by ``get_indicies`` for index ``i``.
    :param i: index of a value to be replaced by a weighted mean of nearby values
    :return: np.array of weights


    """

    out = np.abs(indices - i)  # calculate distance
    out = 2**out  # calculate exponential
    out = 1/out  # calculate inverse

    window = vec[indices]  # see values in window
    out[np.argwhere(np.isnan(window))] = 0

    return out
