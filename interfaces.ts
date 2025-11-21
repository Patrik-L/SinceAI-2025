export interface PositionedItem {
  position: {
    x: number;
    y: number;
    z: number;
  };
  rotation?: {
    pitch: number;
    yaw: number;
    roll: number;
  };
}

export interface SpacialImage extends PositionedItem {
  fov: number;
  imageData: Blob;
}

export interface Device extends PositionedItem {
  id: string;
  name: string;
  colorHex: string;
}

export interface ProcessedImage extends SpacialImage {
  devices: Device[];
}
