import React from 'react';
import ReactDOM from 'react-dom';
import StatusWidget from './containers/status_widget';
import ControlsWidget from './containers/controls';
import ImageWidget from './containers/image_window';
import ColorProfiler from './containers/color_profiler';
import EventsList from './containers/events';

const App = (props) => {
    return(
        <div className="container">
            <div className="row">
                <div className="col-sm-12">
                    <ImageWidget />
                </div>    
            </div>
            <div className="row">
                <div className="col-sm-4">
                    <StatusWidget />
                </div>
                <div className="col-sm-8">
                    <ControlsWidget />
                </div>    
            </div>
            <div className="row">
                <div className="col-sm-12">
                    <ColorProfiler />
                </div>
            </div>
            <div className="row">
                <div className="col-sm-12">
                    <EventsList />
                </div>
            </div>
        </div>
    )
}

ReactDOM.render(<App /> ,document.getElementById('react-root'));