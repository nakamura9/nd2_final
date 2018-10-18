import React from 'react';

const ToggleButton = (props) =>{
    let buttonClass = null;
    let buttonLabel = "";
    if(props.run){
        buttonClass = "btn btn-danger";
        buttonLabel = props.onLabel;
    }else{
        buttonClass = "btn btn-success";
        buttonLabel = props.offLabel;
    }

    return(
        <button
            className={buttonClass}
            onClick={props.toggle}>{buttonLabel}</button>
    )
}

export default ToggleButton;