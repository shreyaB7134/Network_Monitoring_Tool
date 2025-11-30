import speedtest


def run_speed_test():
    try:
        st = speedtest.Speedtest()
        st.get_best_server()
        download = st.download() / 1_000_000
        upload = st.upload() / 1_000_000
        ping = st.results.ping
        return {"download": f"{download:.2f} Mbps", "upload": f"{upload:.2f} Mbps", "ping": f"{ping:.2f} ms", "server": st.results.server.get('name','')}
    except Exception as e:
        return {"error": str(e)}