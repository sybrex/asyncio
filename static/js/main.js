$(function() {
    let ws = new WebSocket('wss://'+$('#host').val()+'/ws');
    ws.onmessage = function(message) {
        data = JSON.parse(message.data);
        data.forEach((game) => {
            update_game(game);
        });
    };
});

function update_game(game) {
    let server_delay = (game.imported - game.generated).toFixed(5);
    let client_time = new Date();
    let client_delay = (client_time.getTime() / 1000 - game.imported.toFixed(3)).toFixed(3);
    if ($('#game_'+game.id).length) {
        if ($('#time_'+game.id) != game.time) {
            $('#time_'+game.id).html(game.time);
        }
        if ($('#home_'+game.id) != game.markets[0]['bets']['1']) {
            update_odds($('#home_'+game.id), game.markets[0]['bets']['1'])
        }
        if ($('#draw_'+game.id) != game.markets[0]['bets']['X']) {
            update_odds($('#draw_'+game.id), game.markets[0]['bets']['X'])
        }
        if ($('#away_'+game.id) != game.markets[0]['bets']['2']) {
            update_odds($('#away_'+game.id), game.markets[0]['bets']['2'])
        }
        if ($('#state_'+game.id) != game.state) {
            $('#state_'+game.id).html(game.state);
        }
        $('#server_delay_'+game.id).html(server_delay);
        $('#client_delay_'+game.id).html(client_delay);
    } else {
        let row = '<tr id="game_'+game.id+'">'
            + '<td id="time_'+game.id+'">'+game.time+'</td>'
            + '<td>'+game.home_team+' - '+game.away_team+'</td>'
            + '<td id="home_'+game.id+'">'+game.markets[0]['bets']['1']+'</td>'
            + '<td id="draw_'+game.id+'">'+game.markets[0]['bets']['X']+'</td>'
            + '<td id="away_'+game.id+'">'+game.markets[0]['bets']['2']+'</td>'
            + '<td id="state_'+game.id+'">'+game.state+'</td>'
            + '<td id="server_delay_'+game.id+'">'+server_delay+'</td>'
            + '<td id="client_delay_'+game.id+'">'+client_delay+'</td>'
            + '</tr>'
        $('#games tbody').append(row);
    }
}

function update_odds(element, odds) {
        if (element.html() != odds) {
            let color = element.html() > odds ? '#dc3545' : '#28a745';
            element.html(odds);
            element.css({'background-color': color});
            element.animate({backgroundColor: '#fff'}, 1000);
        }
    }