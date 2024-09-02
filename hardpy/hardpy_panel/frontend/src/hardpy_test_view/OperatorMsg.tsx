// Copyright (c) 2024 Everypin
// GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

import React, { useEffect, useState } from 'react';
import { Classes, Dialog } from '@blueprintjs/core';

interface StartOperatorMsgDialogProps {
    title: string;
    msg: string;
    onConfirm?: (inputText: string) => void;
}

export function StartOperatorMsgDialog(props: StartOperatorMsgDialogProps) {
    const [dialogOpen, setDialogOpen] = useState(() => {
        const storedValue = localStorage.getItem('dialogOpen');
        return storedValue !== null ? JSON.parse(storedValue) : true;
    });

    const handleClose = () => {
        setDialogOpen(false);
        localStorage.setItem('dialogOpen', JSON.stringify(false));
    };

    useEffect(() => {
        localStorage.setItem('dialogOpen', JSON.stringify(dialogOpen));
    }, [dialogOpen]);

    return (
        <Dialog
            title={props.title || "Message"}
            icon="info-sign"
            isOpen={dialogOpen}
            onClose={handleClose}
            style={{
                width: 'auto',
                height: 'auto',
                minWidth: '300px',
                minHeight: '200px',
                maxWidth: '800px',
            }}
        >
            <div className={Classes.DIALOG_BODY} style={{ wordWrap: 'break-word', wordBreak: 'break-word' }}>
                <p>{props.msg}</p>
            </div>
        </Dialog>
    );
}

export default StartOperatorMsgDialog;