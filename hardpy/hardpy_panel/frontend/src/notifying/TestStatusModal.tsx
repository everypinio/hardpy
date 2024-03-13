// Copyright (c) 2024 Everypin
// GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

import * as React from 'react';
import { Modal } from 'antd';

interface Props {
    modal_open_handler: (is_open: boolean) => void;
}

/**
 * Render status of testesting with modal window
 */
export function StatusNotification(props: Props): React.ReactElement {
    const [isModalVisible, setIsModalVisible] = React.useState(false);
    const [showModal, setShowModal] = React.useState<ReturnType<typeof Modal.success> | undefined>(
        undefined,
    );
    const showModalTimeout = 5 * 1000;
    const handleClose = () => {
        setIsModalVisible(false);
        props.modal_open_handler(false);
    };

    const showModalFailProps = {
        title: 'Test failed!',
        visible: isModalVisible,
        onOk: handleClose,
        okText: 'Accepted',

        onCancel: handleClose,
        cancelText: 'Restart test',
        cancelButtonProps: { disabled: true },
    };

    const showModalSuccessProps = {
        title: 'Testing completed successfully!',
        visible: isModalVisible,
        onOk: handleClose,
        okText: 'Accepted',

        onCancel: handleClose,
        cancelText: '',
        cancelButtonProps: { disabled: true },
    };

    const showModalSkipProps = {
        title: 'Testing interrupted!',
        visible: isModalVisible,
        onOk: handleClose,
        okText: 'Accepted',

        onCancel: handleClose,
        cancelText: '',
        cancelButtonProps: { disabled: true },
    };

    // Run timeout to hide modal
    React.useEffect(() => {
        setTimeout(() => {
            showModal?.destroy();
            props.modal_open_handler(false);
        }, showModalTimeout);
    }, [showModal]);

    /** Render */
    return <></>;
}

export default StatusNotification;
