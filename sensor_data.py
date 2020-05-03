import bme680
import datetime
import time
import logging
class sensor_data:
    def __init__(self, gas_baseline = 0, hum_baseline = 0):
        try:
            self.sensor = bme680.BME680(bme680.I2C_ADDR_PRIMARY)
        except IOError:
            self.sensor = bme680.BME680(bme680.I2C_ADDR_SECONDARY)
        self.sensor.set_gas_heater_temperature(320)
        self.sensor.set_gas_heater_duration(150)
        self.sensor.select_gas_heater_profile(0)
        self.sensor.set_humidity_oversample(bme680.OS_2X)
        self.sensor.set_pressure_oversample(bme680.OS_4X)
        self.sensor.set_temperature_oversample(bme680.OS_8X)
        self.sensor.set_filter(bme680.FILTER_SIZE_3)
        self.sensor.set_gas_status(bme680.ENABLE_GAS_MEAS)
        self.hum_baseline = 50.0
        if gas_baseline != 0:
            self.gas_baseline = gas_baseline
        else:
            start_time = time.time()
            curr_time = time.time()
            burn_in_time = 300
            burn_in_data = []
            logging.info('Starting burn in', extra={'burnintime': burn_in_time})
            try:
                while curr_time - start_time < burn_in_time:
                    curr_time = time.time()
                    if self.sensor.get_sensor_data() and self.sensor.data.heat_stable:
                        gas = self.sensor.data.gas_resistance
                        burn_in_data.append(gas)
                        time.sleep(1)

                self.gas_baseline = sum(burn_in_data[-50:]) / 50.0
                self.hum_baseline = 50.0

                self.hum_weighting = 0.25
            except:
                logging.exception('error with burnin')

    def get_air_quality(self, gas, hum):
        gas_offset = self.gas_baseline - gas
        hum_offset = hum - self.hum_baseline
        if hum_offset > 0:
            hum_score = (100 - self.hum_baseline - hum_offset)
            hum_score /= (100 - self.hum_baseline)
            hum_score *= (self.hum_weighting * 100)
        else:
            hum_score = (self.hum_baseline + hum_offset)
            hum_score /= self.hum_baseline
            hum_score *= (self.hum_weighting * 100)
        if gas_offset > 0:
            gas_score = (gas / self.gas_baseline)
            gas_score *= (100 - (self.hum_weighting * 100))
        else:
            gas_score = 100 - (self.hum_weighting * 100)
        air_quality_score = hum_score + gas_score

        return air_quality_score
    def get_data(self):
        if self.sensor.get_sensor_data() and self.sensor.data.heat_stable:
            return  {
                    "temperature" : '{0:.2f}C'.format(self.sensor.data.temperature),
                    "humidity" : '{0:.2f}'.format(self.sensor.data.humidity),
                    "pressure" : '{0:.2f} hPa'.format(self.sensor.data.pressure),
                    "datetime_utc" : datetime.datetime.utcnow().isoformat(),
                    "gas_resistance" : '{0} Ohms'.format(self.sensor.data.gas_resistance),
                    "air_quality" : '{0}'.format(self.get_air_quality(self.sensor.data.gas_resistance, self.sensor.data.humidity))
                    }
        