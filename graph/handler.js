import 'babel-polyfill';
import { graphqlLambda, graphiqlLambda } from 'apollo-server-lambda';
import { makeExecutableSchema } from 'graphql-tools';
import { schema } from './schema';
import { resolvers } from './resolvers';




const myGraphQLSchema = makeExecutableSchema({
  typeDefs: schema,
  resolvers,
  logger: console,
});


module.exports.graphqlHandler = function graphqlHandler(event, context, callback) {

  context.callbackWaitsForEmptyEventLoop = false;
  function callbackFilter(error, output) {
    if (!output.headers) { output.headers = {}; }

    //eslint-disable-next-line no-param-reassign
    output.headers['Access-Control-Allow-Origin'] = '*';
    callback(error, output);
  }

  const handler = graphqlLambda( { schema: myGraphQLSchema, tracing: true });
  return handler(event, context, callbackFilter);
};


