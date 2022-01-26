import frappe


def update_project_support_hours(doc, method=None):
    """ Update project's support hours based on valid issue """
    if doc.project:
        out = frappe.db.sql("""
            select sum(time_spent) from `tabIssue`
            where project = %s
        """, doc.project)
        total_time = out and out[0][0] or 0
        project = frappe.get_doc("Project", doc.project)
        project.support_hours_used = total_time
        project.save()
    frappe.db.commit()
