$(function() {
    let ws = new WebSocket("ws://localhost:8000/ws");
    ws.onmessage = function(message) {
        event = JSON.parse(message.data);
        if ($('#event_'+event.id).length) {
            if ($('#time_'+event.id) != event.time) {
                $('#time_'+event.id).html(event.time);
            }
            if ($('#home_'+event.id) != event.markets[0]['bets']['1']) {
                update_odds($('#home_'+event.id), event.markets[0]['bets']['1'])
            }
            if ($('#draw_'+event.id) != event.markets[0]['bets']['X']) {
                update_odds($('#draw_'+event.id), event.markets[0]['bets']['X'])
            }
            if ($('#away_'+event.id) != event.markets[0]['bets']['2']) {
                update_odds($('#away_'+event.id), event.markets[0]['bets']['2'])
            }
            if ($('#state_'+event.id) != event.state) {
                $('#state_'+event.id).html(event.state);
            }
        } else {
            let row = '<tr id="event_'+event.id+'">'
                + '<td id="time_'+event.id+'">'+event.time+'</td>'
                + '<td>'+event.home_team+' - '+event.away_team+'</td>'
                + '<td id="home_'+event.id+'">'+event.markets[0]['bets']['1']+'</td>'
                + '<td id="draw_'+event.id+'">'+event.markets[0]['bets']['X']+'</td>'
                + '<td id="away_'+event.id+'">'+event.markets[0]['bets']['2']+'</td>'
                + '<td id="state_'+event.id+'">'+event.state+'</td>'
                + '</tr>'
            $('#events tbody').append(row);
        }
    };
    function update_odds(element, odds) {
        if (element.html() != odds) {
            element.html(odds);
            let color = element.html() > odds ? '#dc3545' : '#28a745';
            element.css({'background-color': color});
            element.animate({backgroundColor: '#fff'}, 1000);
        }
    }
});
