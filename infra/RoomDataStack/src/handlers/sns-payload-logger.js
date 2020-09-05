/**
 * A Lambda function that logs the payload received from SNS.
 */
var AWS = require('aws-sdk');
var dynamodb = new AWS.DynamoDB({apiVersion: '2012-08-10'});

exports.snsPayloadLoggerHandler = async (event, context) => {
    // All log statements are written to CloudWatch by default. For more information, see
    // https://docs.aws.amazon.com/lambda/latest/dg/nodejs-prog-model-logging.html
    const tableName = process.env.DYNAMO_DB_NAME;    
    const message = event.Records[0].Sns.Message;

    const params = {
        TableName: tableName,
        Item:{
            'roomid': message.locationId,
            'datetime': new Date(message.datetime_utc).getTime() / 1000,
            'pressure': message.pressure,
            'gasresistance': message.gas_resistance,
            'temperature' : message.temperature,
            'airquality': message.airquality,
            'humidity':message.humidity
        }
    }
    dynamodb.putItem(params, function(err, data) {
        if (err) {
          console.error("Error", err);
        }
      });
}
