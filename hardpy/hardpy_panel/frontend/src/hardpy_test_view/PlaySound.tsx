// Copyright (c) 2024 Everypin
// GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

import React from "react";
import * as Tone from "tone";

/**
 * Represents a sound with a specific note and duration.
 * @typedef {Object} Sound
 * @property {string} note - The musical note to play (e.g., "C4").
 * @property {number} duration - The delay (in seconds) before the note is played.
 */

type Sound = { note: string; duration: number };

/**
 * Array of sounds to play when a failure occurs.
 * @type {Sound[]}
 */
const FAIL_SOUNDS: Sound[] = [
  { note: "C4", duration: 0 },
  { note: "B3", duration: 0.2 },
];

/**
 * Array of sounds to play when a success occurs.
 * @type {Sound[]}
 */
const SUCCESS_SOUNDS: Sound[] = [
  { note: "C5", duration: 0 },
  { note: "E5", duration: 0.2 },
];

/**
 * The duration (in seconds) for which the sound is sustained.
 * @type {number}
 */
const SOUND_DURATION = 0.3;

/**
 * Props for the PlaySound component.
 * @interface Props
 * @property {string} key - A unique identifier for the component.
 * @property {string} status - The status of the component, which determines the sound to play ("failed" or "passed").
 */
interface Props {
  key: string;
  status: string;
}

/**
 * Plays a sequence of sounds using the Tone.js library.
 * @param {Sound[]} sounds - An array of Sound objects representing the notes to play.
 * @param {number} duration - The duration (in seconds) for which the sound is sustained.
 */
function playSounds(sounds: Sound[], duration: number) {
  const now = Tone.now();
  const synth = new Tone.Synth().toDestination();

  sounds.forEach((sound: Sound) => {
    synth.triggerAttack(sound.note, now + sound.duration);
  });

  synth.triggerRelease(`+${duration}`);
}

/**
 * A React component that plays a sound based on the provided status.
 * @param {Props} props - The props for the PlaySound component.
 * @returns {React.ReactElement} - An empty React element (no visual rendering).
 */
export function PlaySound(props: Props): React.ReactElement {
  /**
   * React effect hook to play sounds when the status changes.
   */
  React.useEffect(() => {
    /**
     * Plays the appropriate sound based on the status.
     */
    const playSound = () => {
      if (props.status == "failed") {
        playSounds(FAIL_SOUNDS, SOUND_DURATION);
      } else if (props.status == "passed") {
        playSounds(SUCCESS_SOUNDS, SOUND_DURATION);
      }
    };

    if (props.status) {
      playSound();
    }
  }, [props.status]);

  return <></>;
}

export default PlaySound;
