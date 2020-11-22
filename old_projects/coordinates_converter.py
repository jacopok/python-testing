from astropy.coordinates import SkyCoord, AltAz, EarthLocation
from astropy.time import Time

pordenone = EarthLocation(lat=45.962068, lon=12.639939)


def ra_dec_to_altaz(right_ascension, declination):

    now = Time.now()
    c = SkyCoord(ra=right_ascension, dec=declination)
    return(c.transform_to(AltAz(obstime=now, location=pordenone)))