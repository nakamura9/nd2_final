import React, {Component} from 'react';
import axios from 'axios';


class StatusWidget extends Component{
    state = {
        status: {
            machineStatus: 'OFF',
            boardCount: 0,
            errorsFound: 0
        }    
    }

    componentDidMount(){
        setInterval(this.tick, 3000);
    }

    tick = () =>{
        axios({
            method: 'GET',
            url: '/api/get-status/'
        }).then(res =>{
            this.setState({status: res.data})
        })
    }

    
    render(){
        return(
            <div className="well">
                <h3>Machine Status</h3>
                <table className="table">
                    <thead>
                        <tr>
                            <th>Parameter</th>
                            <th>Value</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>Machine Status</td>
                            <td>{this.state.status.machineStatus}</td>
                        </tr>
                        <tr>
                            <td>Boards Run</td>
                            <td>{this.state.status.boardCount}</td>
                        </tr>
                        <tr>
                            <td>Errors Found</td>
                            <td>{this.state.status.errorsFound}</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        );
    }
}

export default StatusWidget;