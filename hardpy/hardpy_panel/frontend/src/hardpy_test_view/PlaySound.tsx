// Copyright (c) 2024 Everypin
// GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

import React from 'react';
import * as Tone from 'tone'

type Sound = { note: string, duration: number };

const FAIL_SOUNDS: Sound[] = [
    { note: "C4", duration: 0 },
    { note: "B3", duration: 0.2 }
];

const SUCCESS_SOUNDS: Sound[] = [
    { note: "C5", duration: 0 },
    { note: "E5", duration: 0.2 }
];

const SOUND_DURATION = 0.3;

interface Props {
    key: string
    status: string
}

function playSounds(sounds: Sound[], duration: number) {
    const now = Tone.now()
    const synth = new Tone.Synth().toDestination();

    sounds.forEach((sound: Sound) => {
        synth.triggerAttack(sound.note, now + sound.duration);
    });

    synth.triggerRelease(`+${duration}`);
}

export function PlaySound(props: Props): React.ReactElement {
    /**
     * End sound
     */
    React.useEffect(() => {
        const playSound = () => {
            if (props.status == 'failed') {
                playSounds(FAIL_SOUNDS, SOUND_DURATION);
            } else if (props.status == 'passed') {
                playSounds(SUCCESS_SOUNDS, SOUND_DURATION);
            }
        };

        if (props.status) {
            playSound()
        }
    }, [props.status]);

    return (
        <></>
    );
}

export default PlaySound;
