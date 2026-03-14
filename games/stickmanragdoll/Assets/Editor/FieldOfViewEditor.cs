using UnityEngine;
using UnityEditor;

[CustomEditor(typeof(FieldOfView))]
public class FieldOfViewEditor : Editor
{
    private void OnSceneGUI()
    {
        FieldOfView fov = (FieldOfView)target;
        Handles.color = Color.white;
        Handles.DrawWireArc(fov.transform.position, Vector2.up, Vector2.right, 360, fov.VisionRadius);
        Vector3 viewAngle1 = DirectionFromAngle(fov.transform.eulerAngles.z, -fov.VisionAngle / 2);
        Vector3 viewAngle2 = DirectionFromAngle(fov.transform.eulerAngles.z, fov.VisionAngle / 2);
        Handles.color = Color.red;
        Handles.DrawLine(fov.transform.position, fov.transform.position + viewAngle1 * fov.VisionRadius);
        Handles.DrawLine(fov.transform.position, fov.transform.position + viewAngle2 * fov.VisionRadius);
    }
    private Vector3 DirectionFromAngle(float eulerY, float angleInDegrees)
    {
        angleInDegrees += eulerY;
        return new Vector3(Mathf.Cos(angleInDegrees * Mathf.Deg2Rad), Mathf.Sin(angleInDegrees * Mathf.Deg2Rad), 0);
    }
}