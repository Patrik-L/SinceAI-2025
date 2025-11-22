export interface PositionedItem {
  position: {
    x: number;
    y: number;
    z: number;
  };
  rotation?: number[];
}

export interface SpacialImage extends PositionedItem {
  focalLength: number;
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
