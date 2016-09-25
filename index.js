'use strict';
var Alexa = require('alexa-sdk');

var APP_ID = undefined; //OPTIONAL: replace with "amzn1.echo-sdk-ams.app.[your-unique-value-here]";
var SKILL_NAME = 'Tech Events';

// Empty array
var EVENTS = [];

//***************************************************************************************************************//
exports.handler = function(event, context, callback) {
    var alexa = Alexa.handler(event, context);
    alexa.APP_ID = APP_ID;
    alexa.registerHandlers(handlers);
    alexa.execute();
};

//***************************************************************************************************************//
var handlers = {
	'getWelcomeResponse': function () {
      const sessionAttributes = {};
	    const cardTitle = 'Welcome';
	    const speechOutput = "Welcome to the Alexa tech event finder." +
                        "If you would like to find tech related events please say, " +
                        "Find events";
	    this.emit('LaunchRequest');
	    const repromptText = "If you would like to find tech related events please say, " +
                          "Find events";
	    this.emit('LaunchRequest');
	    const shouldEndSession = false;
    },
    'LaunchRequest': function () {
        this.emit('GetEventInfo');
    },
    'EventIntent': function () {
        this.emit('GetEventInfo');
    },
    'GetEventInfo': function () {
      //api request
      var fs = require('fs');
      var request = require('request');

      var meetup = function() {
        var key = "3355625642612dc66253267606f197e";
        var url = "https://api.meetup.com";

        var composeURL = function(root, object) {
          return root + '?' + JSON.stringify(object).replace(/":"/g, '=').replace(/","/g, '&').slice(2, -2)
        }

        var get = function(params, callback, path) {
          params.key = key;

          request.get(composeURL(url + (path || '/2/open_events'), params), function(err, res, body) {
            if ( err ) {
              console.error(err);
              return false;
            }
            callback(JSON.parse(body)['results']);
            var speechOutput = "There is a meetup called " + name + " at " + time;
            this.emit(':tellWithCard', speechOutput, SKILL_NAME, city, time, name, group);
          })
        }

        var post = function(details, callback, path) {
          details.key = key;
          request.post({
            headers: { 'content-type' : 'application/x-www-form-urlencoded' },
            url: url + (path || '/2/event'),
            form: details
          }, function(err, res, body) {
            callback(body);
          })
        }

        var parseEvent = function(mEvent) {
          /*
           * A simple function that converts JSON to
           * string in a pretty way
          **/
          var time = mEvent['time'] || '';
          var name = mEvent['name'] || '';
          var desc = mEvent['desc'] || '';
          var url = mEvent['url'] || '';

          if ( mEvent['venue']) {
            var city = mEvent['venue']['city'] || '';
          }

          if ( mEvent['group'] )
            var group = mEvent['group']['name'] || '';

          var parsed = '';

          if ( name ) parsed += 'Name: ' + name + '\n';
          if ( city ) parsed += 'City: ' + city + '\n';
          if ( group ) parsed += 'Group: ' + group + '\n';
          if ( time ) parsed += 'Time: ' + time + '\n';
          return parsed;

        };

        var parseEvents = function(results) {
          console.log('a');
          for ( var i = 0; i < results.length; i++ ) {
            console.log( parseEvent(results[i]) );
          }
        }
       return {
          get: get,
          parseEvents: parseEvents,
          post: post
        }
      }

    },
//***************************************************************************************************************/
    'AMAZON.HelpIntent': function () {
        var speechOutput = "You can say tell me a gorilla fact, or, you can say exit... What can I help you with?";
        var reprompt = "What can I help you with?";
        this.emit(':ask', speechOutput, reprompt);
    },
//***************************************************************************************************************//
    'AMAZON.CancelIntent': function () {
        this.emit(':tell', 'Please refer to meetup.com for more information');
    }
};
