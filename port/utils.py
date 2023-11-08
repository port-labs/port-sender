
def get_port_url(region: str, kind: str = "app"):
    if region and region != "eu":
        return f"https://{kind}.{region}.getport.io"
    return f"https://{kind}.getport.io"
