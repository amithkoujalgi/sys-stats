import React, { Component } from 'react';
import axios from 'axios';

class Login extends Component {
  constructor(props) {
    super(props);
    this.state = {
      response: null,
      error: null
    };
  }

  handleSubmit = async () => {
    try {
      const response = await axios.post('http://localhost:8070/api/stats/login', {
        user: 'x',
        password: 'y'
      });
      this.setState({ response: response.data, error: null });
    } catch (error) {
      this.setState({ response: null, error: error.message });
    }
  };

  render() {
    const { response, error } = this.state;

    return (
      <div>
        <button onClick={this.handleSubmit}>Submit</button>
        {response && <div>Response: {JSON.stringify(response)}</div>}
        {error && <div>Error: {error}</div>}
      </div>
    );
  }
}

export default Login;