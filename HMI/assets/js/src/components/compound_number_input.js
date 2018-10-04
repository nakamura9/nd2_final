import React, {Component} from 'react';


class CompoundNumberInput extends Component{
    state = {
        value: 0
    }
    increment = () =>{
        this.setState((prevState) =>{
            return({value: prevState.value + 1})
        }, () => {this.props.handler(this.state.value)})
    }
    decrement = () =>{
        this.setState((prevState) =>{
            return({value: prevState.value - 1})
        }, () => {this.props.handler(this.state.value)})
    }

    handler = (evt) =>{
        this.setState({value: evt.target.value}, 
            () => {this.props.handler(this.state.value)});
    }


    render(){
        return(
            <div>
                <button 
                    onClick={this.decrement}
                    className="btn">-</button>
                <input 
                    value={this.state.value}
                    type="number"
                    onChange={this.handler} />
                <button 
                    onClick={this.increment}
                    className="btn">+</button>
            </div>
        );
    }
}

export default CompoundNumberInput;
