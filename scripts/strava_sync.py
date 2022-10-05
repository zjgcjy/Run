import argparse
import json

from config import JSON_FILE, SQL_FILE, TCX_FOLDER
from generator import Generator


def strava_to_tcx(act_l):
    import os
    from requests import get
    print('')
    for i in act_l:
        try:
            id = i['run_id']
        except NameError as e:
            continue
        fname = os.path.join(TCX_FOLDER, f'{id}.tcx')
        if os.path.exists(fname):
            continue
        url = f'https://www.strava.com/activities/{id}/export_tcx'
        ret = get(url)
        if ret.status_code == 200:
            print('download from ' + url)
            with open(fname, 'wb') as f:
                f.write(ret.content)


def run_strava_sync(client_id, client_secret, refresh_token, tcx=False):
    generator = Generator(SQL_FILE)
    generator.set_strava_config(client_id, client_secret, refresh_token)
    # if you want to refresh data change False to True
    generator.sync(False)

    activities_list = generator.load()
    if tcx:
        strava_to_tcx(activities_list)

    with open(JSON_FILE, "w") as f:
        json.dump(activities_list, f)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("client_id", help="strava client id")
    parser.add_argument("client_secret", help="strava client secret")
    parser.add_argument("refresh_token", help="strava refresh token")
    parser.add_argument("--with-tcx", dest="with_tcx", action="store_true", help="export tcx files")
    options = parser.parse_args()
    run_strava_sync(options.client_id, options.client_secret, options.refresh_token, options.with_tcx)
