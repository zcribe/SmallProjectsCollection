import React from 'react';
import { StyleSheet, Text, View, Button, TouchableOpacity, Timer } from 'react-native';
import {vibrate} from './utils'

let timer;
let change;
let timerRestMode = false;
const timerWorkMinutes = 25;
const timerWorkSeconds = 0;
const timerRestMinutes = 5;
const timerRestSeconds = 0;
const timerDelay = 1000;


export default class App extends React.Component {
  constructor(){
    super();
    this.state = {
      restMode: timerRestMode,
      timerSeconds:timerWorkSeconds,
      timerMinutes:timerWorkMinutes,
    };
 }

  timerSet = () =>{
    this.timerMode;
    timer = setInterval(this.timerUpdate, timerDelay);
  };

  timerStop = () => {
    clearInterval(timer);
  };


  timerReset = () => {
    clearInterval(timer);
    timer = null;
    this.timerMode();
  };

  timerUpdate = () => {
    if (this.state.timerSeconds === 0 && this.state.timerMinutes === 0 ) {
      this.timerReset();
      vibrate();
      this.state.restMode = !this.state.restMode;
      this.timerMode();
    } else {
      this.timerUnits();
    };
  };

  timerUnits = () => {
    if (this.state.timerSeconds === 0) {
      this.setState({
        restMode: this.state.restMode,
        timerMinutes: this.state.timerMinutes - 1,
        timerSeconds: 59,
      })
    } else {
      this.setState({timerSeconds: this.state.timerSeconds - 1})
    }
  }

  timerMode = () => {
    if (this.state.restMode === false){
      this.setState({
        restMode: false,
        timerSeconds:timerWorkSeconds,
        timerMinutes:timerWorkMinutes,
      })
    } else {
      this.setState({
        restMode: true,
        timerSeconds:timerRestSeconds,
        timerMinutes:timerRestMinutes,
      })
    }
  }

  timerValuePad = (val) => {
    if (val < 10){
      return "0".concat(val.toString())
    } else {
      return val
    }
  }




  render() {
    return (
	<View style={styles.container}>
	
    <View>
		<Text style={styles.timerLabel} >{this.state.timerMinutes}:{this.timerValuePad(this.state.timerSeconds)}</Text>
    </View>
	<View style={styles.buttonGroup}>
		<TouchableOpacity
         style={[styles.button, styles.start]}
         onPress={this.timerSet}
		>
         <Text style={styles.textWhite}> Start </Text>
       </TouchableOpacity>
	   <TouchableOpacity
         style={[styles.button, styles.stop]}
         onPress={this.timerStop}
		>
         <Text style={styles.textWhite}> Stop </Text>
       </TouchableOpacity>
	   <TouchableOpacity
         style={[styles.button, styles.reset]}
         onPress={this.timerReset}
		>
         <Text style={styles.textWhite}> Reset </Text>
       </TouchableOpacity>
	   
		</View>
		<View style={styles.appTitleContainer}>
			<Text style={styles.appTitle}>Pomodoro Timer</Text>
		</View>
	</View>
    );
  }
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  }, button: {
    alignItems: 'center',
    backgroundColor: '#DDDDDD',
    padding: 20,
	color:'#fff',
  }, buttonGroup: {
	  flexDirection: 'row',
	  padding: 40,
  }, timerLabel: {
	  fontWeight: '700',
	  fontSize:90,
	  color: '#4b6584',
  }, start: {
	  backgroundColor: '#26de81',
  }, stop: {
	  backgroundColor: '#fc5c65',
  }, reset: {
	  backgroundColor: '#45aaf2',
  }, textWhite: {
	  color: '#fff',
	  fontWeight: '700',
  }, appTitle: {
	  color: '#dfe4ea',
  }, appTitleContainer: {
	  justifyContent: 'flex-end',
  }
});









function timerSet(){
  timer = setInterval(this.timerUpdate, timerDelay);
};

function timerStop() {
  clearInterval(timer);
};


function timerReset() {
  clearInterval(timer);
  timer = null

function timerUpdate() {
  this.App.state.timerValue += 1000;
  if (timerValue >= timerWork) {
    this.timerReset();
    vibrate();
  }
};
}