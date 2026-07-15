/**
 * SSE 流式通信模块
 */

const SSE = {
    eventSource: null,
    isConnecting: false,

    /**
     * 连接 SSE 流
     * @param {string} sessionId - 会话 ID
     * @param {string} message - 用户消息
     * @param {Function} onChunk - 接收到数据块的回调
     * @param {Function} onDone - 完成的回调
     * @param {Function} onError - 错误的回调
     */
    connect(sessionId, message, onChunk, onDone, onError) {
        // 关闭现有连接
        this.close();

        this.isConnecting = true;

        // 构建 URL（SSE 只支持 GET，参数放在 URL 中）
        const params = new URLSearchParams({
            session_id: sessionId,
            message: message
        });
        const url = `http://localhost:8000/api/v1/chat/stream?${params.tostring()}`;

        try {
            this.eventSource = new EventSource(url);

            // 监听消息
            this.eventSource.onmessage = (event) => {
                try {
                    const data = JSON.parse(event.data);

                    switch (data.type) {
                        case 'start':
                            console.log('SSE 流开始');
                            break;
                        case 'chunk':
                            if (onChunk) onChunk(data.content);
                            break;
                        case 'departments':
                            if (onChunk) onChunk('', data.data);
                            break;
                        case 'done':
                            this.close();
                            if (onDone) onDone();
                            break;
                    }
                } catch (error) {
                    console.error('解析 SSE 数据失败：', error);
                }
            };

            // 监听错误
            this.eventSource.onerror = (error) => {
                console.error('SSE 连接错误：', error);
                this.close();
                if (onError) onError(error);
            };

        } catch (error) {
            console.error('创建 SSE 连接失败：', error);
            if (onError) onError(error);
        }
    },

    /**
     * 关闭 SSE 连接
     */
    close() {
        if (this.eventSource) {
            this.eventSource.close();
            this.eventSource = null;
        }
        this.isConnecting = false;
    }
};

// 导出
if (typeof module !== 'undefined' && module.exports) {
    module.exports = SSE;
}
