import React from 'react';
import Lobby from './Lobby';
const ws = new WebSocket('ws://localhost:3000/ws');

export default class MainPage extends React.Component {
  constructor(props){
    super(props)
    this.state = {
      game_id : null,
      open_games : [],
    }
  }

  componentDidMount(){
    ws.onopen = () => {
      console.log('socket opened');
    }

    ws.onmessage = (message) => {
      const data = JSON.parse(message.data)
      const { type } = data
      const { game_id, player, games: open_games, move, message : serverMessage } = data.data
      switch(type) {
        case 'new-game':
          console.log('NEW GAME - GAME ID: ', game_id)
          this.setState(({ game_id }))
          break;
        case 'joined-game': 
          console.log(serverMessage)
          this.setState(({ game_id }))
          break;
        case 'open-games':
          this.setState(({ open_games }))
          break;
        default:
          break;
      }
    }
  }

  handleCreateGame = (e) => {
    e.preventDefault();

    const message = {
      type : 'new-game'
    }

    ws.send(JSON.stringify(message));
  }

  render(){
    return (
      <div>
        <Lobby open_games={this.state.open_games} handleCreateGame={this.handleCreateGame}/>
      </div>
    )
  }
}