import React, {Component} from 'react';
import RadioControls from '../components/mode_radio_controls';
import ToggleButton from '../components/toggle_button';
import CompoundNumberInput from '../components/compound_number_input';
import axios from 'axios';
import $ from 'jquery';

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
        this.setState({printerOne: value});
    }

    printerTwoHandler = (value) =>{
        this.setState({printerTwo: value});
       
    }

    setRegister = () =>{
        console.log(this.state.printerOne);
        axios.post('/api/get-register-positions',
        {
            'unitTwo': this.state.printerOne,
            'unitOne': this.state.printerTwo
        }
        );
    }

    render(){
        let controls = null;
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
        
        return(
            <div className="well">
                {controls}
                <button 
                    className="btn btn-primary"
                    onClick={this.setRegister}>
                    Register Changes
                </button>
            </div>
        )
    }
}

export default ControlsWidget;