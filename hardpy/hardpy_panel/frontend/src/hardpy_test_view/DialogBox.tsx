import React, { useState } from 'react';
import { Button, Classes, Dialog } from '@blueprintjs/core';

interface Props {
    title_bar: string;
    dialog_text: string;
    onConfirm?: () => void;
    width?: string;
}

export function StartConfirmationDialog(props: Props) {

    const [dialogOpen, setDialogOpen] = useState(true);

    const handleClose = () => {
        setDialogOpen(false);
    };

    const handleConfirm = () => {
        setDialogOpen(false);
        if (props.onConfirm) {
            props.onConfirm();
        }
    };

    const defaultWidth = '500px';
    const dialogWidth = props.width || defaultWidth;

    return (
        <Dialog
            title={props.title_bar}
            icon="info-sign"
            isOpen={dialogOpen}
            onClose={handleClose}
            style={{ width: dialogWidth }}
        >
            <div className={Classes.DIALOG_BODY}>
                <p>{props.dialog_text}</p>
            </div>
            <div className={Classes.DIALOG_FOOTER}>
                <Button intent="primary" onClick={handleConfirm}>Confirm</Button>
            </div>
        </Dialog>
    );
}

export default StartConfirmationDialog