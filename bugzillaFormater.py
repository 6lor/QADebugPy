import argparse
import requests


def get_bugs(in_s, out_f):
    out_f = out_f.upper()
    g_bugs = requests.get("https://us-bz3.devzing.com/gotenna/rest/bug?include_fields=id,summary,severity,resolution",
                          params={"id": in_s, "api_key": "INSERT BUGZILLA TOKEN"})
    if g_bugs.status_code == 200:
        if out_f == "NONE":
            for item in g_bugs.json()['bugs']:
                print("{} - {}\t| {}".format(item['id'],
                                              item['summary'],
                                              item['severity'][0].upper() + item['severity'][1:]))

        elif out_f == "TR":
            for item in g_bugs.json()['bugs']:
                print("||[{i}](https://us-bz3.devzing.com/gotenna/show_bug.cgi?id={i}) - {sum}\t| {sev}"
                      .format(i=item['id'],
                              sum=item['summary'],
                              sev=item['severity'][0].upper() + item['severity'][1:]))
        elif out_f == "GD":
            for item in g_bugs.json()['bugs']:
                
                if item['resolution'] == "":
                    item['resolution'] = "--"

                print('=HYPERLINK("https://us-bz3.devzing.com/gotenna/show_bug.cgi?id={i}","{i}")\t{res}\t{sum}'
                      .format(i=item['id'],
                              sum=item['summary'],
                              res=item['resolution']))
        else:
            print("How did you get here?")
    else:
        print("Response code is not 200, or it timed out.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='PROG')
    parser.add_argument("input", metavar="string-input",
                        help="String of Bug IDs divided by commas, no spaces please")
    parser.add_argument("-o", "--output", default="none",
                        help="Output types, by default none. Options: tr, gd, none.",
                        choices=["tr", "gd", "none"])
    settings = parser.parse_args()
    get_bugs(settings.input, settings.output)
