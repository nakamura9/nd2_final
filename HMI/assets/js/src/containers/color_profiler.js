import React, {Component} from 'react';
import ToggleButton from '../components/toggle_button';
import RadioControls from '../components/mode_radio_controls';
import axios from 'axios';


class ColorProfiler extends Component{
    state = {
        currentColor: "",
        status: {
            currentColor: {
                red: 0,
                green: 0,
                blue: 0
            },
            status: "OFF"
        },
        mode: "auto",
        setColor: {
            red: 0,
            green: 0,
            blue: 0
        },
        pigmentValve: false,
        baseValve: false,
        agitator: true
    }
    componentDidMount(){
        //setInterval(this.tick, 3000);
    }

    tick = () =>{
        axios({
            method: 'GET',
            url: '/api/get-color-status',
        }).then(res => {
            this.setState({status: res.data})
        })
    }
    modeHandler = (evt) =>{
        axios({
            method: 'GET',
            url: '/api/toggle-color-mode',
        })
        this.setState({mode: evt.target.value});
    }

    pigmentToggle = () =>{
        axios({
            method: 'GET',
            url: '/api/toggle-pigment-valve',
        });
        this.setState((prevState) =>{
            return({pigmentValve: !prevState.pigmentValve})
        });
    }

    baseToggle = () =>{
        axios({
            method: 'GET',
            url: '/api/toggle-base-valve',
        });
        this.setState((prevState) =>{
            return({baseValve: !prevState.baseValve})
        })
    }

    agitatorToggle = () =>{
        axios({
            method: 'GET',
            url: '/api/toggle-agitator',
        })
        this.setState((prevState) =>{
            return({agitator: !prevState.agitator})
        })
    }

    updateSetColor = () => {
        axios.post('/api/set-color-setpoint/',
            this.state.setColor
        )
    }
    setColorHandler = (evt) =>{
        const colorName = evt.target.name;
        const colorValue = evt.target.value;
        let newSetColor = this.state.setColor;
        console.log('progress');
        if(colorValue >= 0 && colorValue < 256){
            newSetColor[colorName] = evt.target.value;
            this.setState({setColor: newSetColor});
        }else{
            alert('Please insert a value less than 256 ');
        }
    }


    render(){
        let controls = null;
        controls = 
                <div>
                    <h4>Color Profiler State</h4>
                    <h5>Pigment Valve</h5>
                    <ToggleButton 
                        run={this.state.pigmentValve}
                        toggle={this.pigmentToggle}
                        onLabel='Close'
                        offLabel='Open'/>
                    <h5>Base Valve</h5>
                    <ToggleButton 
                        run={this.state.baseValve}
                        toggle={this.baseToggle}
                        onLabel='Close'
                        offLabel='Open'/>

                    <h5>Agitator</h5>
                    <ToggleButton 
                        run={this.state.agitator}
                        toggle={this.agitatorToggle}
                        onLabel='Close'
                        offLabel='Open'/>           
                </div>
        
        return(
            <div className="well">
                <h3>Color Profiler</h3>
                <h4>Status:</h4>
                <table className="table">
                    <thead>
                        <tr>
                            <th>Parameter</th>
                            <th>Value</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>Status</td>
                            <td>{this.state.status.status}</td>
                        </tr>
                        <tr>
                            <td>Current Color Value</td>
                            <td><ul>
                                    <li>Red: {this.state.status.currentColor.red}</li>
                                    <li>Green: {this.state.status.currentColor.green}</li>
                                    <li>Blue: {this.state.status.currentColor.blue}</li>
                                </ul></td>
                        </tr>
                        
                    </tbody>
                </table>
                <h5>Color Set Point</h5>
                <span>Red(0-255)</span><input 
                        className="form-control"
                        onChange={this.setColorHandler}
                        placeholder="rrr"
                        type="number"
                        name="red"
                        value={this.state.setColor.red}
                        /><br />
                <span>Green(0-255)</span><input 
                        className="form-control"
                        onChange={this.setColorHandler}
                        placeholder="ggg"
                        type="number"
                        name="green"
                        value={this.state.setColor.green}
                        /><br />
                <span>Blue(0-255)</span><input 
                        className="form-control"
                        onChange={this.setColorHandler}
                        placeholder="bbb"
                        type="number"
                        name="blue"
                        value={this.state.setColor.blue}
                        /><br />
                <button className="btn btn-success"
                    onClick={this.updateSetColor}>
                    Set Color</button>
                {controls}
            </div>
        );
    }
}

export default ColorProfiler;