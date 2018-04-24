import React from 'react';
const ws = new WebSocket('ws://localhost:3000/ws')


export default class MainPage extends React.Component {
  constructor(props){
    super(props)
    this.state = {
      'game_id' : '',
      'type' : ''
    }

  }

  componentDidMount(){
    ws.onopen = () => {
      console.log('socket opened')
    };

    ws.onmessage = (message) => {
      console.log(message.type, message.data)
    }
  }

  handleSendMessage = (e) => {
    e.preventDefault();

    const input = e.target.elements.input.value.trim();
    ws.send(input);
  }

  createNewGame = (e) => {
    e.preventDefault();

    const message = {
      type: "new-game"
    }

    ws.send(JSON.stringify(message));
  }

  handleJoinGame = (e) => {
    e.preventDefault();

    const game_id = e.target.elements.game_id.value.trim();
    const join_game = {
      'type' : 'join_game',
      game_id
    }

    ws.send(JSON.stringify(join_game));
  }

  render(){
    return (
      <div>
        <p></p>
        <form onSubmit={this.handleSendMessage}>
          <input type="text" name="input" />
          <button>Send Message</button>
        </form>
        <form onSubmit={this.createNewGame}>
          <button>Create new game!</button>
        </form>
        <form onSubmit={this.handleJoinGame}>
          <input type="text" name="game_id"/>
          <button>Join Game!</button>
        </form>
      </div>
    )
  }
}