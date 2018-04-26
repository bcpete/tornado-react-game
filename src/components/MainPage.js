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
      console.log(data)
      if(data.data.game_id){
        this.setState(({ game_id : data.data.game_id }));
      }else if(data.type === 'open-games'){
        this.setState(({ open_games : data.data.games }));
        console.log(this.state.open_games)
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
        <Lobby games={this.state.open_games} handleCreateGame={this.handleCreateGame}/>
      </div>
    )
  }
}