import bme680
import datetime
import time
class sensor_data:
    def __init__(self, gas_baseline = 0, hum_baseline = 0):
        try:
            self.sensor = bme680.BME680(bme680.I2C_ADDR_PRIMARY)
        except IOError:
            self.sensor = bme680.BME680(bme680.I2C_ADDR_SECONDARY)
        sensor.set_gas_heater_temperature(320)
        sensor.set_gas_heater_duration(150)
        sensor.select_gas_heater_profile(0)
        sensor.set_humidity_oversample(bme680.OS_2X)
        sensor.set_pressure_oversample(bme680.OS_4X)
        sensor.set_temperature_oversample(bme680.OS_8X)
        sensor.set_filter(bme680.FILTER_SIZE_3)
        sensor.set_gas_status(bme680.ENABLE_GAS_MEAS)
        self.hum_baseline = 50.0
        if gas_baseline != 0:
            self.gas_baseline = gas_baseline
        else:
            start_time = time.time()
            curr_time = time.time()
            burn_in_time = 300
            burn_in_data = []
            try:
                print('Collecting gas resistance burn-in data for 5 mins\n')
                while curr_time - start_time < burn_in_time:
                    curr_time = time.time()
                    if sensor.get_sensor_data() and sensor.data.heat_stable:
                        gas = sensor.data.gas_resistance
                        burn_in_data.append(gas)
                        print('Gas: {0} Ohms'.format(gas))
                        time.sleep(1)

                self.gas_baseline = sum(burn_in_data[-50:]) / 50.0
                self.hum_baseline = 50.0

                hum_weighting = 0.25
    def get_air_quality(self, gas, hum):
        gas_offset = gas_baseline - gas
        hum_offset = hum - hum_baseline
        if hum_offset > 0:
            hum_score = (100 - hum_baseline - hum_offset)
            hum_score /= (100 - hum_baseline)
            hum_score *= (self.hum_weighting * 100)
        else:
            hum_score = (hum_baseline + hum_offset)
            hum_score /= hum_baseline
            hum_score *= (self.hum_weighting * 100)
        if gas_offset > 0:
            gas_score = (gas / gas_baseline)
            gas_score *= (100 - (self.hum_weighting * 100))
        else:
            gas_score = 100 - (self.hum_weighting * 100)
        air_quality_score = hum_score + gas_score

        return air_quality_score
    def getData(self, locationname):
        if sensor.get_sensor_data() and sensor.data.heat_stable:
            response = {
                    "location_name" : locationname,
                    "temperature" : '{0:.2f}C'.format(sensor.data.temperature),
                    "humidity" : '{0:.2f}'.format(sensor.data.humidity),
                    "pressure" : '{0:.2f} hPa'.format(sensor.data.pressure),
                    "datetime_utc" : datetime.datetime.utcnow().isoformat(),
                    "gas_resistance" : '{0},{1} Ohms'.format(sensor.data.gas_resistance),
                    "air_quality" : '{0}'.format(get_air_quality(sensor.data.gas_resistance, sensor.data.humidity))
                    }
        return response
        