exports.handler = async function (event) {
  const token = event.authorizationToken.toLowerCase()
  const methodArn = event.methodArn

  switch (token) {
    case 'allow':
      return generateAuthResponse('user', 'Allow', methodArn)
    default:
      return generateAuthResponse('user', 'Deny', methodArn)
  }
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