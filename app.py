
import os
import pandas as pd

import etl.assessment
import model
import viz.map
import params
# run etl if needed

# run model if needed

# run viz to show model results


def run_app():
    assess_data = os.path.join(params.data_dir, params.assessment_data)
    pts = pd.concat([i for i in etl.assessment.process(f=assess_data)])
    viz.map.add_map(pts)


if __name__ == "__main__":

    run_app()
