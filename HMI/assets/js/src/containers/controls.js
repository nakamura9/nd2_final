import React, {Component} from 'react';
import RadioControls from '../components/mode_radio_controls';
import ToggleButton from '../components/toggle_button';
import CompoundNumberInput from '../components/compound_number_input';
import axios from 'axios';

class ControlsWidget extends Component{
    state = {
        mode: 'auto',
        run: false,
        printerOne: 0,
        printerTwo: 0
    }

    modeHandler = (evt) =>{
        axios({
            method: 'GET',
            url: '/api/toggle-machine-mode'
        });
        this.setState({mode: evt.target.value});
    }

    runToggle = () =>{
        //make a request to the server to toggle the machine
        axios({
            method: 'GET',
            url: '/api/toggle-printer',
        });
        this.setState((prevState) =>{
            return({run: !prevState.run})
        });
    }
    
    printerOneHandler = (value) =>{
        axios({
            method: 'GET',
            url: '/api/get-register-positions',
            data: {
                'unitOne': value,
                'unitTwo': 0
            }
        });
        this.setState({printerOne: value});
    }

    printerTwoHandler = (value) =>{
        this.setState({printerTwo: value});
        axios({
            method: 'GET',
            url: '/api/get-register-positions',
            data: {
                'unitTwo': value,
                'unitOne': 0
            }
        });
    }

    render(){
        let controls = null;
        if(this.state.mode == "auto"){
            controls = 
                <div>
                    <h3>Auto Mode enabled</h3>
                    <p>Corrections of prints are currently being handled automatically .Set Mode to manual for greater control of machine operation.</p>
                </div>                  
        }else{
            controls = 
                <div>
                    <h3>Printer State</h3>
                    <ToggleButton 
                        run={this.state.run}
                        toggle={this.runToggle}
                        onLabel='Stop'
                        offLabel='Run'/>
                    <h3>Print Roller Positions</h3>
                    <h5>Printer 1</h5>
                    <CompoundNumberInput 
                        handler={this.printerOneHandler}/>
                    <h5>Printer 2</h5>
                    <CompoundNumberInput 
                        handler={this.printerTwoHandler}/>
                </div>
        }
        return(
            <div className="well">
                <RadioControls 
                    handler={this.modeHandler}/>
                    
                {controls}
            </div>
        )
    }
}

export default ControlsWidget;