function plotSentiment(posSent, negSent, neutSent, mixedSent) {
    var data = [{
        values: [posSent,negSent,neutSent,mixedSent],
        labels: ['Positive Sentiment', 'Negative Sentiment', 'Neutral Sentiment', 'Mixed Sentiment'],
        type: 'pie'
        }];
    var layout = {
        height: 500,
        width: 600
    };
    Plotly.newPlot('viz', data, layout, align = "center");
}

const getResp = function() {
    var requestData = document.getElementById("textInput").value;
    console.log(requestData);
    fetch('https://c24ge3u77j.execute-api.us-east-1.amazonaws.com/prod/helloworld',{
        method: 'POST',
        body: JSON.stringify
        ({text: requestData}),
        headers: {
            'Content-type': 'application/json; charset=UTF-8'
        }
    }).then(function(response){
        console.log(response);
        return response.json();
    }).then(function(data){
        var outputRes = data.body;
        console.log(outputRes);
        var positiveSent = outputRes.Positive * 100;
        console.log(positiveSent);
        var negativeSent = outputRes.Negative * 100;
        var neutralSent = outputRes.Neutral * 100;
        var mixedSent = outputRes.Mixed * 100
        var currElem = document.getElementById("sentButton");
        plotSentiment(positiveSent, negativeSent, neutralSent, mixedSent);
    }).catch(function(error) {
        console.warn('Something went wrong', error);
    })
};