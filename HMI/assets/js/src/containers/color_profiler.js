import React, {Component} from 'react';
import ToggleButton from '../components/toggle_button';
import RadioControls from '../components/mode_radio_controls';
import axios from 'axios';


class ColorProfiler extends Component{
    state = {
        currentColor: "",
        setColor: "",
        status: {
            currentColor: "",
            status: "OFF"
        },
        mode: "auto",
        setColor: "",
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


    setColorHandler = (evt) =>{
        axios({
            method: 'GET',
            url: '/api/set-color-setpoint',
            data: {'color': evt.target.value}
        })
        this.setState({setColor: evt.target.value});
    }


    render(){
        let controls = null;
        if(this.state.mode == "auto"){
            controls = 
                <div>
                    <h4>Auto Mode enabled</h4>
                    <p>Corrections of color deviations are currently being handled automatically .Set Mode to manual for greater control of color profiler.</p>
                </div>                  
        }else{
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
        }
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
                            <td>{this.state.status.currentColor}</td>
                        </tr>
                        <tr>
                            <td>Set Color Value</td>
                            <td>{this.state.setColor}</td>
                        </tr>
                    </tbody>
                </table>
                <h5>Color Set Point</h5>
                <input 
                        className="form-control"
                        onChange={this.setColorHandler}
                        placeholder="rrrgggbbb"
                        type="text"
                        />
                <RadioControls 
                    handler={this.modeHandler}/>
                {controls}
            </div>
        );
    }
}

export default ColorProfiler;