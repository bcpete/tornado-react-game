import React from 'react';
const ws = new WebSocket('ws://localhost:3000/ws')


export default class MainPage extends React.Component {
  constructor(props){
    super(props)
    this.state = {
      message: ''
    }

  }

  componentDidMount(){
    ws.onopen = () => {
      ws.send('Hello World');
      console.log(ws)
    };

    ws.onmessage = (message) => {
      this.setState(({ message: message.data }));
    }
  }

  handleSendMessage = (e) => {
    e.preventDefault();

    const input = e.target.elements.input.value.trim();
    ws.send(input);
  }

  render(){
    return (
      <div>
        <p>{this.state.message}</p>
        <form onSubmit={this.handleSendMessage}>
          <input type="text" name="input" />
          <button>Send Message</button>
        </form>
      </div>
    )
  }
}