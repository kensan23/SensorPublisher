/**
 * A Lambda function that logs the payload received from SNS.
 */
var AWS = require("aws-sdk");
var docClient = new AWS.DynamoDB.DocumentClient({ apiVersion: "2012-08-10" });
parseNum = str => +str.replace(/[^.\d]/g, '');

exports.snsPayloadLoggerHandler = async (event, context) => {
  // All log statements are written to CloudWatch by default. For more information, see
  // https://docs.aws.amazon.com/lambda/latest/dg/nodejs-prog-model-logging.html
  const tableName = process.env.DYNAMO_DB_NAME;
  const messageRaw = event.Records[0].Sns.Message;
  const message = JSON.parse(messageRaw);
  const params = {
    TableName: tableName,
    Item: {
      roomid: message.locationId,
      datetimeunix: new Date(message.datetime_utc).getTime() / 1000,
      pressure_hPa: parseNum(message.pressure),
      gasresistance_Ohms: parseNum(message.gas_resistance),
      temperature_C: parseNum(message.temperature),
      airquality_percent: parseNum(message.air_quality),
      humidity_percent: parseNum(message.humidity),
    },
  };

  try {
    await docClient.put(params).promise();
  } catch (e) {
    console.error("Error", e);
  }
};
