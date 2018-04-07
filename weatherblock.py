#!/home/trst2284/.local/share/virtualenvs/noaablocks-nPJEcr8f/bin/python3


# TODO eventually we'll have a cli instead of this terrible script.
def main():
    try:
        forecast = get_hourly_forecast(*get_location())
        temp, next_temp = get_current_temp(forecast)
    except:
        print("{'full_text': 'ERROR'}")
        return

    json_dict = {
        'full_text': '{} {} {} degrees'.format(temp, '->', next_temp)
    }

    print(json.dumps(json_dict))
    return


if __name__ == '__main__':
    try:
        import json

        from noaablocks.weather import get_hourly_forecast, get_location, get_current_temp

        main()
    except Exception as e:
        with open('/tmp/error.log', 'a') as f:
            f.write('{}'.format(e))
            try:
                import sys
                f.write('{}'.format(sys.executable))
            except:
                pass

        print("{\"full_text\": \"ERROR\"}")
