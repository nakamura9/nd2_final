import React, {Component} from 'react';
import axios from 'axios';

class EventsList extends Component{
    state = {
        events: []
    }
    componentDidMount(){
        //setInterval(this.tick, 1000);
    }

    tick = () =>{
        axios({
            method: 'GET',
            url: '/api/get-events/'
        }).then(res =>{
            this.setState({events: res.data['events']});
        });
    }
    render(){
        return(
            <div className="well">
                <h3>List of Events</h3>
                <ul>
                    {this.state.events.map((evt,i) =>(
                        <li key={i}>{evt}</li>
                    ))}
                </ul>
            </div>
        )
    }
}

export default EventsList;