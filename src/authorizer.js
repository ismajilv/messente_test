exports.handler = async function (event) {
  const token = event.authorizationToken//.toLowerCase()

  var encodedCreds = token.split(' ')[1]
  var plainCreds = (new Buffer(encodedCreds, 'base64')).toString().split(':')
  var username = plainCreds[0]
  var password = plainCreds[1]
  console.log(username, password)

  const methodArn = event.methodArn

  console.log(password === 'piret')

  if ((username === 'messente' && password === 'piret') || (username === 'piret' && password === 'messente')) return generateAuthResponse(username, 'Allow', methodArn)
  else return generateAuthResponse(username, 'Deny', methodArn)
}

function generateAuthResponse (principalId, effect, methodArn) {
  // If you need to provide additional information to your integration
  // endpoint (e.g. your Lambda Function), you can add it to `context`
  const context = {
    'stringKey': 'stringval',
    'numberKey': 123,
    'booleanKey': true
  }
  const policyDocument = generatePolicyDocument(effect, methodArn)

  return {
    principalId,
    context,
    policyDocument
  }
}

function generatePolicyDocument (effect, methodArn) {
  if (!effect || !methodArn) return null

  const policyDocument = {
    Version: '2012-10-17',
    Statement: [{
      Action: 'execute-api:Invoke',
      Effect: effect,
      Resource: methodArn
    }]
  }

  return policyDocument
}