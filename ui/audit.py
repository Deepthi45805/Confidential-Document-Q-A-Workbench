import streamlit as st
import pandas as pd
from database.audit_log import AuditLogger

def render_audit():
    st.title("📋 Local Audit Log")
    st.markdown("Compulsory local compliance trail recording timestamps, invoking agents, and documents touched.")

    audit_logger = AuditLogger()

    if st.button("Clear Audit Logs"):
        audit_logger.clear_logs()
        st.success("Audit log cleared.")
        st.rerun()

    logs = audit_logger.get_all_logs(limit=200)

    if logs:
        df = pd.DataFrame(logs)
        df = df[["id", "timestamp", "user_request", "selected_agent", "routing_reason", "documents_accessed", "status", "execution_time_ms"]]
        
        st.dataframe(
            df,
            column_config={
                "id": "ID",
                "timestamp": "Timestamp",
                "user_request": "User Query",
                "selected_agent": "Invoked Agent",
                "routing_reason": "Routing Reason",
                "documents_accessed": "Documents Touched",
                "status": "Status",
                "execution_time_ms": st.column_config.NumberColumn("Latency (ms)", format="%.1f ms")
            },
            use_container_width=True
        )
    else:
        st.info("No audit entries available yet.")
