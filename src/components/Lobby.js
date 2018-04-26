import React from 'react';

const Lobby = (props) => (
  <div>
    <h1>Join/Start a Game!</h1>
    <div>
      {props.games.length === 0 &&
        <h3>No open games :(</h3>
      }
      {
        props.games.map((game) => (
          <p key={game} >{ game }</p>
        ))
      }
      <form onSubmit={(e) => props.handleCreateGame(e)}>
        <button>Create a Game</button>
      </form>
    </div>
  </div>
)

export default Lobby;